const express = require('express');
const path = require('path');
const apiRoutes = require('./src/routes/api');

const app = express();

app.use(express.static('public'));
app.use('/api', apiRoutes);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/linkvertise-return', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'linkvertise-return.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
