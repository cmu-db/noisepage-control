import * as React from 'react';
import { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import axios from '../../util/axios';

export default function WorkloadContent({ databaseId }) {
  const [workloads, setWorkloads] = useState();
  
  useEffect(() => {
    async function fetchWorkloads() {
      try {
        const res = await axios.get(`/database_manager/workload/${databaseId}`);
        console.log(res);
        setWorkloads(res.data);  
      } catch (error) {
        console.error(error)
      }
    }
    fetchWorkloads();
  }, [databaseId]);

  return workloads && (
    <React.Fragment>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Workload ID</TableCell>
              <TableCell>Workload Name</TableCell>
              <TableCell>Available</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {workloads.map((workload) => (
              <TableRow
                key={workload.resource_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {workload.resource_id}
                </TableCell>
                <TableCell>{workload.resource_name}</TableCell>
                <TableCell>{workload.available.toString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Button variant="contained" startIcon={<LibraryAdd />} sx={{ mt: 3 }}>
        Collect New Workload
      </Button>
    </React.Fragment>
  )
}
