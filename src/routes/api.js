const express = require('express');
const router = express.Router();
const hwidService = require('../services/hwidService');
const linkvertiseService = require('../services/linkvertiseService');

router.get('/check-hwid', hwidService.checkHWID);
router.get('/generate-key', linkvertiseService.generateKey);

module.exports = router;
