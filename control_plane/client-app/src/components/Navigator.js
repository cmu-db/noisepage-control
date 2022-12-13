import * as React from 'react';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import DnsRoundedIcon from '@mui/icons-material/DnsRounded';
import AddIcon from '@mui/icons-material/AddBox';
import SettingsIcon from '@mui/icons-material/Settings';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { NavLink } from 'react-router-dom';

const tabs = [
  {
    name: 'View Databases',
    icon: <DnsRoundedIcon />,
    link: '/databases'
  },
  {
    name: 'Register Database',
    icon: <AddIcon />,
    link: '/register',
  },
  {
    name: 'Settings',
    icon: <SettingsIcon />,
    link: '/settings',
  }
]

const item = {
  py: '2px',
  px: 3,
  color: 'rgba(255, 255, 255, 0.7)',
  '&:hover, &:focus': {
    bgcolor: 'rgba(255, 255, 255, 0.08)',
  },
};

const itemCategory = {
  boxShadow: '0 -1px 0 rgb(255,255,255,0.1) inset',
  py: 1.5,
  px: 3,
};

export default function Navigator(props) {
  const { ...other } = props;

  const [activeTabId, setActiveTabId] = React.useState(0);

  return (
    <Drawer variant="permanent" {...other}>
      <List disablePadding sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
        <ListItem sx={{ ...item, ...itemCategory, fontSize: 22, color: '#fff', flexDirection: 'column' }}>
          <img src='/noisepage-horizontal.svg' style={{ width: '200px', height: '80px' }} />
          {"\n"}
          <Typography variant="h5" sx={{ my: 1 }}>Gym Control Plane</Typography>
        </ListItem>
        {tabs.map(({ name, icon, link }, tabId) => (
          <ListItem sx={{ display: 'flex' }} disablePadding key={name}>
            <NavLink to={link} style={{ textDecoration: 'none', flex: '1' }}>
              <ListItemButton sx={item} selected={activeTabId === tabId} onClick={() => {setActiveTabId(tabId)}}>
                <ListItemIcon>{icon}</ListItemIcon>
                <ListItemText>{name}</ListItemText>
              </ListItemButton>
            </NavLink>
          </ListItem>
        ))}
        {/* <Divider sx={{ my: 0.5 }} /> */}
        <ListItem sx={{ display: 'flex', justifyContent: 'center', my: 0.5 }} disablePadding>
          <Typography variant="caption" color='GrayText' display="block" gutterBottom>
            Build Version: 66203b6a1df
          </Typography>
        </ListItem>
        <div style={{ flex: '1' }}>
        </div>
        <ListItem sx={{ display: 'flex', justifyContent: 'center' }} disablePadding>
          <Typography sx={{ fontSize: '0.9rem', color: '#4caf50', display: 'flex', alignItems: 'center' }} variant="caption" color='success.main' display="block" gutterBottom>
            <span style={{
              height: '6px',
              width: '6px',
              backgroundColor: '#4caf50',
              borderRadius: '50%',
              display: 'inline-block',
              marginRight: '10px'
            }}></span>Status: Online
          </Typography>
        </ListItem>
        <ListItem sx={{ display: 'flex', marginBottom: '10px' }}>
          <NavLink to='/' style={{ textDecoration: 'none', flex: '1' }}>
            <ListItemButton sx={{ ...item, textAlign: 'center', bgcolor: 'rgba(255, 255, 255, 0.05)' }} onClick={() => {setActiveTabId(1)}}>
              <ListItemIcon sx={{ position: 'absolute' }}><AccountCircleIcon /></ListItemIcon>
              <ListItemText>User Account</ListItemText>
            </ListItemButton>
          </NavLink>
        </ListItem>
      </List>
    </Drawer>
  );
}