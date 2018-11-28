const express = require('express');
const app = express();
const commits = require('./models/commits');
const port = '9006';

function getCommit() {
  chosenOne = commits.messagesArray[Math.floor(Math.random() * commits.messagesArray.length)];
  return chosenOne;
}

//app.get('/yolo', (req, res) => res.status(200).json({ status: 200, name: getCommit() }));
app.get('/yolo', (req, res) => res.status(200).send( getCommit() ));
app.listen(port, () => console.log('yolo running on port ' + port));
