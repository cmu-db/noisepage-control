import * as React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Header from '../../components/Header';
import DatabaseInfo from './DatabaseInfo';
import axios from '../../util/axios';

function ViewDatabases() {
  const [databaseInfos, setDatabaseInfos] = useState();

  useEffect(() => {
    async function fetchDatabaseInfos() {
      const res = await axios.get('/database_manager/databases');
      console.log(res);
      setDatabaseInfos(res.data);
    }
    fetchDatabaseInfos();
  }, []);

  const renderSortedDatabaseInfos = () => {
    const infos = [...databaseInfos];
    infos.sort((a, b) => new Date(b.created) - new Date(a.created));
    return infos.map((info, index) => <DatabaseInfo key={info.database_id} databaseInfo={info} index={index} />);
  }

  return (
    <React.Fragment>
      <Header title="Active Databases" />
      <Box component="main" sx={{ flex: 1, py: 6, px: 6 }}>
        {databaseInfos && renderSortedDatabaseInfos()}
      </Box>
    </React.Fragment>
  )
};

export default ViewDatabases;
