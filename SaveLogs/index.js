
const MongoClient = require("mongodb").MongoClient;
const MONGODB_URI = "mongodb+srv://" + process.env.adminmbd + ":" + process.env.passwordmbd + "@ssatrust.rrthf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
let cachedDb = null;

async function connectToDatabase() {
    if (cachedDb) {

        return cachedDb;
    }

    const client = await MongoClient.connect(MONGODB_URI);
    const db = await client.db('EnhancingTrust');
    cachedDb = db;
    return db
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
        date: new Date()
    };
    const result = await db.collection("savedLogs").insertOne(inputLog);
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