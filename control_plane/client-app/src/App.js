import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navigator from './components/Navigator';
import RegisterDatabase from './pages/RegisterDatabases';
import MyDatabases from './pages/MyDatabases';
import ManageDatabase from './pages/ManageDatabase';
import DetailContent from './pages/ManageDatabase/DetailContent';
import WorkloadContent from './pages/ManageDatabase/WorkloadContent';
import StateContent from './pages/ManageDatabase/StateContent';
import TuneDatabaseContent from './pages/ManageDatabase/TuneDatabaseContent';
import TuningHistoryContent from './pages/ManageDatabase/TuningHistoryContent';
import theme from './theme';

function Copyright() {
  return (
    <Typography variant="body2" color="white" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://db.cs.cmu.edu/">
        Carnegie Mellon University Database Group,
      </Link>{' '}
      {new Date().getFullYear()}.
    </Typography>
  );
}

const drawerWidth = 256;

export default function App() {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const isSmUp = useMediaQuery(theme.breakpoints.up('sm'));

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Box sx={{ display: 'flex', minHeight: '100vh' }}>
          <Box
            component="nav"
            sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
          >
            {isSmUp ? null : (
              <Navigator
                PaperProps={{ style: { width: drawerWidth } }}
                variant="temporary"
                open={mobileOpen}
                onClose={handleDrawerToggle}
              />
            )}

            <Navigator
              PaperProps={{ style: { width: drawerWidth } }}
              sx={{ display: { sm: 'block', xs: 'none' } }}
            />
          </Box>
          <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#eaeff1', backgroundImage: 'url(/db-skulls.svg)' }}>
            <Routes>
              <Route path="/" exact element={<Navigate to="/databases" />} />
              <Route path="/register" element={<RegisterDatabase />} />
              <Route path="/databases" element={<MyDatabases />} />
              <Route path="/databases/:id" element={<ManageDatabase />} >
                <Route index element={<Navigate to="tune" />} />
                <Route path="details" element={<DetailContent />} />
                <Route path="tune" element={<TuneDatabaseContent />} />
                <Route path="tuning-history" element={<TuningHistoryContent />} />
                <Route path="workloads" element={<WorkloadContent />} />
                <Route path="states" element={<StateContent />} />
              </Route>
            </Routes>
            <Box component="footer" sx={{ p: 2, bgcolor: '#565658' }}>
              <Copyright />
            </Box>
          </Box>
        </Box>
      </BrowserRouter>
    </ThemeProvider>
  );
}