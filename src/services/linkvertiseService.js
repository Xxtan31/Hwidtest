const fetch = require('node-fetch');
const generateRandomKey = require('../utils/keyGenerator');
const hwidService = require('./hwidService');

const LINKVERTISE_API_URL = 'https://publisher.linkvertise.com/api/v1/redirect/link/';
const LINKVERTISE_USER_ID = '1208943';

exports.generateKey = async (req, res) => {
    const hwid = req.query.hwid;
    const linkvertiseId = req.query.linkvertise_id;

    try {
        const isCompleted = await checkLinkvertiseCompletion(linkvertiseId);
        if (isCompleted) {
            const key = generateRandomKey();
            hwidService.setKey(hwid, key);
            res.json({ status: 'success', key: key });
        } else {
            res.json({ status: 'error', message: 'LinkVertise not completed' });
        }
    } catch (error) {
        console.error('Error in generateKey:', error);
        res.status(500).json({ status: 'error', message: 'Internal server error' });
    }
};

async function checkLinkvertiseCompletion(linkvertiseId) {
    try {
        const response = await fetch(`${LINKVERTISE_API_URL}${LINKVERTISE_USER_ID}/${linkvertiseId}/stats`);
        const data = await response.json();
        return data.data.clicks > 0;
    } catch (error) {
        console.error('Error checking LinkVertise completion:', error);
        return false;
    }
}
