const express = require('express');

const app = express();

app.listen(3000, () => {
    console.log('listening for request on port 3000');
});

app.get('/', (req, res) => {
    console.log('request made');
    res.send('Hello World!');
});