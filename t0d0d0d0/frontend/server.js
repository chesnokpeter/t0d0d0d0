import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 8101;

app.use(express.static(path.join(__dirname, 'dist')));

app.use(express.static(path.join(__dirname, 'src/assets')));


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.get('/overview', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.get('/projects', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.get('/tasks', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.use(express.static(path.join(__dirname, 'dist')));

app.listen(port, () => {
    console.log(`http://localhost:${port}`);
});