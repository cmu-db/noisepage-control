import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://ec2-3-87-186-24.compute-1.amazonaws.com:8000'
});

export default instance;
