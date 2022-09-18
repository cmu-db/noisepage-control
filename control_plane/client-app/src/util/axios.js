import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    // 'Access-Control-Allow-Origin': 'http://localhost:8000',
  }
});

export default instance;
