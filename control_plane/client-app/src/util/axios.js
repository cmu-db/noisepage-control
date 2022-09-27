import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://ec2-34-207-82-72.compute-1.amazonaws.com:8000'
});

export default instance;
