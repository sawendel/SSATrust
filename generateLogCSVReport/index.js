const { Parser } = require('json2csv');
const MongoClient = require("mongodb").MongoClient;

let cachedDb = null;

async function connectToDatabase() {
    if (cachedDb) {
        return cachedDb;
    }

    const MONGODB_URI = `mongodb://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:27017/${process.env.DB_NAME}?retryWrites=true&w=majority`;
    console.log(MONGODB_URI);
    const client = await MongoClient.connect(MONGODB_URI);
    const db = await client.db(process.env.DB_NAME);
    cachedDb = db;

    return db
}

exports.handler = async (event, context) => {
    context.callbackWaitsForEmptyEventLoop = false;
    const db = await connectToDatabase();  
    
    const startDate = event.queryStringParameters.startDate;
    const endDate = event.queryStringParameters.endDate;
    
    const result = await db.collection(process.env.DB_COLLECTION).find({
        created: {
            '$gte': new Date(new Date(startDate).setHours(0,0,0,0)),
            '$lte': new Date(new Date(endDate).setHours(0,0,0,0)),
        },
    }).sort({ created: -1 }).toArray();
    
    const fields = [
        '_id',
        'userId',
        'eventType',
        'metadata',
        'workflowId',
        'templateName',
        'templateType',
        'created',
    ];
    const parser = new Parser({ fields });
    const csv = parser.parse(result);
    const response = {
        statusCode: 200,
        headers: {
            'Content-Disposition': `attachment; filename="logs_${+new Date()}.csv"`,
        },
        body: csv,
    };
    
    return response;
};
