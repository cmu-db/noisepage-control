import * as React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Header from '../../components/Header';
import Content from '../../components/Content';
import DatabaseInfo from './DatabaseInfo';
import axios from '../../util/axios';

function MyDatabases() {
  const [databaseInfos, setDatabaseInfos] = useState();

  useEffect(() => {
    async function fetchDatabaseInfos() {
      const res = await axios.get('/database_manager/');
      console.log(res);
      setDatabaseInfos(res.data);
    }
    fetchDatabaseInfos();
  }, []);

  return (
    <React.Fragment>
      <Header title="My Databases" />
      <Box component="main" sx={{ flex: 1, py: 6, px: 6, bgcolor: '#eaeff1' }}>
        {console.log(databaseInfos)}
        {databaseInfos && databaseInfos.map((databaseInfo) => (
          <DatabaseInfo key={databaseInfo.database_id} databaseInfo={databaseInfo} />
        ))}
      </Box>
    </React.Fragment>
  )
};

export default MyDatabases;
