from confluent_kafka import Consumer
import json, os, asyncio
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import asyncpg
from dataclasses import dataclass
from typing import List

load_dotenv(find_dotenv())

KAFKA_BOOTSTRAP = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
TOPIC = os.environ.get('TOPIC')
POSTGRES_DSN = os.environ.get('POSTGRES_DSN')
__CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')))
__CONSUMER = Consumer(__CONFIG)
__CONSUMER.subscribe([TOPIC])

@dataclass
class Transaction:
    transaction_id: str
    user_id: int
    amount: float
    timestamp: str
    is_fraud: bool

class PostgresProcessor:
    def __init__(self, batch_size=5):
        self.batch_size = batch_size
        self.batch: List[Transaction] = []
        self.pool = None
    
    async def init_db(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(POSTGRES_DSN)
        
        # Create table if not exists
        async with self.pool.acquire() as conn:
            await conn.execute(open(os.path.join(os.path.dirname(__file__), '..', 'db', 'init.sql')).read())
        print("✅ Database initialized")
    
    async def save_batch(self, batch: List[Transaction]):
        """Save a batch of transactions to PostgreSQL"""
        if not batch:
            return
        try:
            async with self.pool.acquire() as conn:
                # Prepare the batch insert
                values = []
                for tx in batch:
                    values.append((
                        tx.transaction_id, tx.user_id, tx.amount, 
                        tx.timestamp, tx.is_fraud
                    ))
                
                # Batch insert using executemany
                await conn.executemany('''
                    INSERT INTO transactions 
                    (transaction_id, user_id, amount, timestamp, is_fraud)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (transaction_id) DO NOTHING
                ''', values)
                
                print(f"💾 Saved batch of {len(batch)} transactions")
                
                # Log fraud transactions
                fraud_count = sum(1 for tx in batch if tx.is_fraud)
                if fraud_count > 0:
                    print(f"🆘 Detected {fraud_count} fraudulent transactions in batch")
                    
        except Exception as e:
            print(f"💥 Error saving batch: {e}")
    
    def add_to_batch(self, data: dict) -> bool:
        """Add transaction to batch, return True if batch is full"""
        tx = Transaction(
            transaction_id=data['transaction_id'],
            user_id=data['user_id'],
            amount=data['amount'],
            timestamp=data['timestamp'],
            is_fraud=data['amount'] > 3000.0
        )
        
        self.batch.append(tx)
        
        # Log individual transaction
        fraud_msg = "🆘 Fraud Detected!" if tx.is_fraud else ""
        print(f"✅ Consumed: {tx.transaction_id} (Amount: ${tx.amount}, Fraud: {tx.is_fraud}) {fraud_msg}")
        
        return len(self.batch) >= self.batch_size
    
    async def process_batch_if_ready(self):
        """Process batch if it's full"""
        if len(self.batch) >= self.batch_size:
            batch_to_process = self.batch.copy()
            self.batch.clear()
            await self.save_batch(batch_to_process)
    
    async def flush_remaining(self):
        """Process any remaining transactions in the batch"""
        if self.batch:
            await self.save_batch(self.batch)
            self.batch.clear()



async def consume():
    print("🚀 Starting Transaction Consumer with Async Batch Processing...")
    
    # Initialize batch processor
    processor = PostgresProcessor(batch_size=5)
    await processor.init_db()
    
    start_time = datetime.now()
    processed_count = 0
    
    try:
        while True:
            msg = __CONSUMER.poll(1.0)
            current_time = datetime.now()
            
            if msg is None:
                # Check if we need to process partial batch due to timeout
                if (current_time - start_time).total_seconds() > 30 and processor.batch:
                    print("⏰ Timeout reached, processing partial batch...")
                    await processor.process_batch_if_ready()
                    start_time = current_time
                    print(f"⌛️ Waiting for new messages...")
                continue
            
            if msg.error():
                print(f"❌ Consumer error: {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                processed_count += 1
                
                # Add to batch and check if batch is ready
                batch_ready = processor.add_to_batch(data)
                
                if batch_ready:
                    await processor.process_batch_if_ready()
                    start_time = current_time  # Reset timer
                
                # Manually commit offset for each message
                __CONSUMER.commit(msg)
                
            except Exception as e:
                print(f"💥 Error processing message: {e}")
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping consumer...")
    except Exception as e:
        print(f"💥 Consumer error: {e}")
    finally:
        # Process any remaining transactions
        await processor.flush_remaining()
        print(f"📊 Total messages processed: {processed_count}")
        __CONSUMER.close()

if __name__ == "__main__":
    asyncio.run(consume())