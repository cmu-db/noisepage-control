import * as React from 'react';
import Box from '@mui/material/Box';
import Header from '../../components/Header';
import Content from '../../components/Content';

function MyDatabases() {
  return (
    <React.Fragment>
      <Header title="My Databases" />
      <Box component="main" sx={{ flex: 1, py: 6, px: 4, bgcolor: '#eaeff1' }}>
        <Content />
      </Box>
    </React.Fragment>
  )
};

export default MyDatabases;
