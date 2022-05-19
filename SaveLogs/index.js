
const MongoClient = require("mongodb").MongoClient;

let cachedDb = null;

async function connectToDatabase() {
    if (cachedDb) {
        return cachedDb;
    }

    const MONGODB_URI = `mongodb://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:27017/${process.env.DB_NAME}?retryWrites=true&w=majority`;
    const client = await MongoClient.connect(MONGODB_URI);
    const db = await client.db(process.env.DB_NAME);
    cachedDb = db;
    return db
}

async function processEvent(event) {
    
}

exports.handler = async (event, context) => {
    context.callbackWaitsForEmptyEventLoop = false;
    const db = await connectToDatabase();   

    var body = JSON.parse(event.body);
    const inputLog = {
        userId: body.userId,
        eventType: body.eventType,
        workflowId: body.workflowId,
        templateName: body.templateName,
        templateType: body.templateType,
        created: new Date()
    };
    const result = await db.collection(process.env.DB_COLLECTION).insertOne(inputLog);
    const response = {
        statusCode: 200,
        headers: { 
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'*',
            'Access-Control-Allow-Headers':'*',
        },
        body: JSON.stringify(result),
    };
    return response;
};
