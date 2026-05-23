


# 🍃 MongoDB Complete Learning Guide

[![MongoDB](https://img.shields.io/badge/MongoDB-4.4%2B-green)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)


## Table of Contents

1. [What is MongoDB?](#what-is-mongodb)
2. [MongoDB Structure](#mongodb-structure)
3. [SQL vs NoSQL Comparison](#sql-vs-nosql-comparison)
4. [Installation & Setup](#installation--setup)
5. [Database & Collection Operations](#database--collection-operations)
6. [CRUD Operations](#crud-operations)
7. [Data Types in MongoDB](#data-types-in-mongodb)
8. [Operators](#operators)
9. [Aggregation Framework](#aggregation-framework)
10. [Data Modeling & Relationships](#data-modeling--relationships)
11. [Schema Validation](#schema-validation)
12. [Indexes](#indexes)
13. [Transactions](#transactions)
14. [Replication](#replication)
15. [Sharding](#sharding)
16. [Interview Questions & Answers](#interview-questions--answers)

## 1. What is MongoDB?

MongoDB is a NoSQL database that stores data in flexible, JSON-like documents (actually BSON). It is designed for:

- Scalability – easy horizontal scaling
- Performance – high-speed reads/writes
- Flexibility – schema-less design
- Unstructured data – handles semi-structured data efficiently

**History:** First released in 2009 by company 10gen (later renamed MongoDB, Inc.)

## 2. MongoDB Structure

MongoDB organizes data using the following hierarchy:

- **Database**
  - **Collection** (like a table)
  - **Document** (like a row)
  - **Field** (like a column, key-value pair)

Example Document:

```json
{
  "_id": 1,
  "name": "Raju",
  "email": "raju@example.com",
  "age": 35,
  "address": {
    "street": "123 Bollywood Blvd",
    "city": "Mumbai"
  },
  "hobbies": ["acting", "reading"]
}
```

## 3. SQL vs NoSQL Comparison

| Feature | NoSQL (MongoDB) | SQL (RDBMS) |
|---|---|---|
| Scalability | Horizontal (add servers) | Vertical (add resources to one server) |
| Schema | Schema-less, flexible | Predefined, rigid |
| Performance | Faster for large/unstructured data | Slower with complex joins |
| Data handling | Unstructured/semi-structured | Structured data |
| Joins | $lookup (less efficient) | Native JOINs |

## 4. Installation & Setup

Default port: `27017`

Change port:

```bash
mongod --port 27019
```

Basic commands after installation:

```bash
mongod # Start MongoDB server
mongo # Start MongoDB shell
```

## 5. Database & Collection Operations

### Database Commands

```javascript
use database_name // Create/switch to database
show dbs // List all databases
db.dropDatabase() // Delete current database
```

### Collection Commands

```javascript
db.createCollection("myCollection") // Create collection
show collections // List collections
db.collection_name.drop() // Drop collection
```

## 6. CRUD Operations

### CREATE

```javascript
db.collection.insertOne({ name: "Raju", age: 25 })
db.collection.insertMany([
  { name: "Sham", age: 28 },
  { name: "Baburao", age: 45 }
])
```

### READ

```javascript
db.collection.find() // All documents
db.collection.find({ age: 25 }) // With filter
db.collection.findOne({ name: "Raju" }) // Single document
```

### UPDATE

```javascript
// Update one document
db.cars.updateOne(
  { model: "Nexon" },
  { $set: { color: "Red" } }
)

// Update many
db.cars.updateMany(
  { model: "Nexon" },
  { $set: { fuel_type: "Electric" } }
)

// Update nested field
db.cars.updateOne(
  { model: "Nexon" },
  { $set: { "engine.cc": 1300 } }
)

// Array operations
db.cars.updateOne(
  { model: "Nexon" },
  { $push: { features: "Heated Seats" } }
)

db.cars.updateOne(
  { model: "Nexon" },
  { $pull: { features: "Bluetooth" } }
)

// Add multiple array values
db.cars.updateOne(
  { model: "Nexon" },
  { $push: { features: { $each: ["Wireless", "Voice Control"] } } }
)

// Upsert (insert if not exists)
db.students.updateMany(
  { name: "Jane Doe" },
  { $set: { age: 22 } },
  { upsert: true }
)
```

### DELETE

```javascript
db.collection.deleteOne({ name: "Raju" })
db.collection.deleteMany({ age: { $lt: 18 } })
```

## 7. Data Types in MongoDB

| Type | Example |
|---|---|
| ObjectId | `ObjectId("507f1f77bcf86cd799439011")` |
| String | `"John Doe"` |
| Integer | `30` |
| Double | `19.99` |
| Boolean | `true` |
| Array | `["mongodb", "database"]` |
| Object | `{ street: "123 Main St" }` |
| Date | `ISODate("2023-08-21T14:23:00Z")` |
| Null | `null` |
| Timestamp | `Timestamp(1638306013, 1)` |
| Decimal128 | `Decimal128("12345.67")` |

## 8. Operators

### Comparison Operators

| Operator | Meaning | Example |
|---|---|---|
| `$eq` | Equal | `{ age: { $eq: 25 } }` |
| `$lt` | Less than | `{ age: { $lt: 30 } }` |
| `$gt` | Greater than | `{ age: { $gt: 20 } }` |
| `$lte` | Less than or equal | `{ age: { $lte: 30 } }` |
| `$gte` | Greater than or equal | `{ age: { $gte: 18 } }` |
| `$ne` | Not equal | `{ age: { $ne: 25 } }` |
| `$in` | In array | `{ age: { $in: [20, 30] } }` |

### Logical Operators

```javascript
// AND
db.collection.find({
  $and: [
    { fuel_type: "Diesel" },
    { features: "Turbocharged" }
  ]
})

// OR
db.collection.find({
  $or: [
    { transmission: "Automatic" },
    { features: "Sunroof" }
  ]
})

// NOR (neither)
db.collection.find({
  $nor: [
    { transmission: "Automatic" },
    { features: "Sunroof" }
  ]
})
```

### Element Operators

```javascript
{ age: { $exists: true } } // Field exists
{ name: { $type: "string" } } // Field type is string
```

### Array Operators

```javascript
db.collection.find({ hobbies: { $size: 4 } }) // Exact array size
db.collection.find({ hobbies: { $all: ["play", "read"] } }) // Contains all
```

### Cursor Methods

```javascript
db.collection.find().count() // Count documents
db.collection.find().sort({ name: 1 }) // 1 = ascending, -1 = descending
db.collection.find().limit(2) // Limit results
db.collection.find().skip(3) // Skip documents
```

## 9. Aggregation Framework

Aggregation processes data through a pipeline of stages.

### Syntax

```javascript
db.collection.aggregate([
  { stage1 },
  { stage2 },
  // ...
])
```

### Common Stages

| Stage | Purpose |
|---|---|
| `$match` | Filter documents (like WHERE) |
| `$group` | Group by a key with accumulators |
| `$project` | Reshape documents (include/exclude fields) |
| `$sort` | Sort documents |
| `$limit` | Limit number of documents |
| `$skip` | Skip documents |
| `$unwind` | Deconstruct array into multiple documents |
| `$lookup` | Left join with another collection |
| `$addFields` / `$set` | Add new fields |
| `$count` | Count documents |
| `$out` | Save results to a new collection |

### Examples

#### Grouping - Count cars by brand

```javascript
db.cars.aggregate([
  {
    $group: {
      _id: "$maker",
      TotalCars: { $sum: 1 }
    }
  }
])
```

#### Match + Group

```javascript
db.cars.aggregate([
  { $match: { maker: "Hyundai" } },
  {
    $group: {
      _id: "$fuel_type",
      TotalCars: { $sum: 1 }
    }
  }
])
```

#### Project + Concat

```javascript
db.cars.aggregate([
  { $match: { maker: "Hyundai" } },
  {
    $project: {
      CarName: { $concat: ["$maker", " ", "$model"] }
    }
  }
])
```

#### Unwind (flatten arrays)

```javascript
db.cars.aggregate([
  { $unwind: "$owners" }
])
```

#### String Operators

```javascript
// Regex match
db.cars.aggregate([
  {
    $project: {
      is_diesel: {
        $regexMatch: { input: "$fuel_type", regex: "Die" }
      }
    }
  }
])
```

#### Arithmetic Operators

```javascript
db.cars.aggregate([
  {
    $project: {
      price: { $add: ["$price", 50000] }
    }
  }
])
```

#### Conditional Logic - $cond

```javascript
db.cars.aggregate([
  {
    $project: {
      fuelCategory: {
        $cond: {
          if: { $eq: ["$fuel_type", "Petrol"] },
          then: "Petrol Car",
          else: "Non-Petrol Car"
        }
      }
    }
  }
])
```

#### Conditional Logic - $switch

```javascript
db.cars.aggregate([
  {
    $project: {
      priceCategory: {
        $switch: {
          branches: [
            { case: { $lt: ["$price", 500000] }, then: "Budget" },
            { case: { $lt: ["$price", 1000000] }, then: "Midrange" }
          ],
          default: "Premium"
        }
      }
    }
  }
])
```

#### Save output to a collection

```javascript
db.cars.aggregate([
  { $match: { maker: "Hyundai" } },
  { $out: "hyundai_cars" }
])
```

### Accumulators in `$group`

- `$sum` - Sum of values
- `$avg` - Average
- `$min` - Minimum
- `$max` - Maximum
- `$push` - Array of all values
- `$addToSet` - Array of unique values

## 10. Data Modeling & Relationships

### Relationship Types

- One-to-One (1:1)
- One-to-Many (1:N)
- Many-to-Many (N:N)

### Two Approaches

#### A. Embedded Documents (Denormalization)

```javascript
{
  "_id": "user1",
  "name": "Amit Sharma",
  "orders": [
    { "product": "Laptop", "amount": 50000 },
    { "product": "Mobile", "amount": 15000 }
  ]
}
```

- ✅ Pros: Better read performance, single query
- ❌ Cons: 16MB document limit, data duplication

#### B. Referenced Documents (Normalization)

```javascript
// users collection
{ "_id": "user1", "name": "Amit Sharma" }

// orders collection
{ "_id": "order1", "user_id": "user1", "product": "Laptop" }
```

Join with `$lookup`:

```javascript
db.users.aggregate([
  {
    $lookup: {
      from: "orders",
      localField: "_id",
      foreignField: "user_id",
      as: "orders"
    }
  }
])
```

- ✅ Pros: No duplication, normalized data
- ❌ Cons: Multiple queries or joins, slower

### Limits

- Maximum document size: 16 MB
- Maximum nesting depth: 100 levels

## 11. Schema Validation

### Create collection with validation

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "age"],
      properties: {
        name: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        age: {
          bsonType: "int",
          minimum: 18,
          description: "must be integer >= 18"
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})
```

### Add validation to existing collection

```javascript
db.runCommand({
  collMod: "users",
  validator: { $jsonSchema: { ... } },
  validationLevel: "moderate",
  validationAction: "warn"
})
```

### Validation Levels

- `strict` – All documents must comply
- `moderate` – Only new/modified documents validated

### Validation Actions

- `error` – Reject invalid operations
- `warn` – Log warning but allow operation

## 12. Indexes

### What is an Index?

An index is a data structure that improves query speed by allowing MongoDB to find documents without scanning every document.

### Commands

```javascript
db.collection.createIndex({ field: 1 }) // Ascending index
db.collection.createIndex({ field: -1 }) // Descending index
db.collection.createIndex({ field: 1 }, { unique: true }) // Unique index
db.collection.dropIndex("field_1") // Drop index
db.collection.getIndexes() // List all indexes
```

### Types of Indexes

| Index Type | Description |
|---|---|
| Single Field | Index on one field |
| Compound | Index on multiple fields |
| Unique | Prevents duplicate values |
| Multikey | For array fields |
| Text | For text search |
| Geospatial | For location-based queries |
| TTL (Time to Live) | Auto-delete after expiration |

### Performance Considerations

- ⚡ Reads: Faster with indexes
- 🐢 Writes: Slower (indexes must be updated)
- 💾 RAM: Indexes should fit in RAM for best performance

## 13. Transactions

Multi-document transactions provide ACID compliance across multiple documents/collections.

### Example (Money Transfer)

```javascript
const session = db.getMongo().startSession();
session.startTransaction();

try {
  db.accounts.updateOne(
    { account: "A" },
    { $inc: { balance: -1000 } }
  );
  db.accounts.updateOne(
    { account: "B" },
    { $inc: { balance: 1000 } }
  );
  session.commitTransaction();
} catch (error) {
  session.abortTransaction();
} finally {
  session.endSession();
}
```

## 14. Replication

A Replica Set is a group of MongoDB servers with identical copies of data.

### Components

- **Primary Node** – Handles all writes
- **Secondary Nodes** – Replicate data from primary
- **Arbiter** – Votes in elections (no data)

### Benefits

- ✅ High availability (automatic failover)
- ✅ Redundancy
- ✅ Read scalability (secondary reads)

## 15. Sharding

Sharding distributes data across multiple servers (shards) for horizontal scaling.

### Components

- **Shards** – Store actual data
- **Config Servers** – Store metadata
- **Mongos** – Query router

### Benefits

- Handle very large datasets
- High throughput operations
- Linear scalability

## 16. Interview Questions & Answers

### Q1: What is MongoDB?
**A:** A NoSQL database that stores data in flexible, JSON-like documents (BSON), allowing schema-less data storage with horizontal scalability.

### Q2: How is MongoDB different from RDBMS?
**A:** MongoDB uses collections & documents (vs tables & rows), has a flexible schema, scales horizontally, and handles unstructured data better.

### Q3: What is a Replica Set?
**A:** A group of MongoDB instances maintaining the same data. One primary handles writes and multiple secondaries handle reads and failover. Provides high availability.

### Q4: What is Sharding?
**A:** Distributing data across multiple servers to enable horizontal scaling for large datasets and high throughput.

### Q5: What is the _id field?
**A:** A mandatory unique identifier for each document. It cannot be removed, but it can be modified (not recommended).

### Q6: insert() vs insertMany()?
**A:** `insert()` inserts one document; `insertMany()` inserts multiple documents in one operation (more efficient for bulk inserts).

### Q7: updateOne() vs updateMany() vs replaceOne()?
- `updateOne` – Updates the first matching document
- `updateMany` – Updates all matching documents
- `replaceOne` – Replaces the entire document

### Q8: Embedding vs Referencing?
- Embedding – Better read performance, but has a 16MB limit and may duplicate data.
- Referencing – Normalized, no duplication, but requires joins or extra queries.

### Q9: What is a TTL Index?
**A:** A Time-to-Live index automatically deletes documents after a specified period. Useful for sessions, logs, and caches.

### Q10: How to optimize a MongoDB query?
- Create appropriate indexes
- Use projections (return only needed fields)
- Use `explain()` to analyze queries
- Avoid full collection scans
- Consider denormalization for frequent reads

### Q11: What is the Aggregation Framework?
**A:** A pipeline-based data processing framework with stages like `$match`, `$group`, `$project`, and `$lookup` for complex transformations.

### Q12: How does MongoDB handle concurrency?
**A:** Uses the WiredTiger storage engine with document-level locking, plus journaling for durability.

### Q13: Backup and restore?

```bash
mongodump --db mydb # Backup
mongorestore --db mydb # Restore
```

### Q14: MongoDB Atlas vs On-premises?
- Atlas – Fully managed cloud service (automated scaling, backups, security).
- On-premises – Manual management of hardware, scaling, backups.

### Q15: What is journaling?
**A:** A mechanism that logs write operations before applying them, ensuring durability and crash recovery.

### Pros of MongoDB

- Flexible schema
- Horizontal scaling
- High performance for reads/writes
- Rich query language & aggregation
- Automatic failover

### Limitations

- No native JOINs (use `$lookup`)
- 16MB document limit
- Transactions only in later versions
- No foreign key constraints
