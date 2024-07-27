const express = require('express');
const router = express.Router();
const path = require('path');

router.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../../public', 'index.html'));
});

router.get('/linkvertise-return', (req, res) => {
    res.sendFile(path.join(__dirname, '../../public', 'linkvertise-return.html'));
});

module.exports = router;
