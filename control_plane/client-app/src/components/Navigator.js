import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DnsRoundedIcon from '@mui/icons-material/DnsRounded';
import SettingsIcon from '@mui/icons-material/Settings';
import { NavLink } from 'react-router-dom';

const tabs = [
  {
    name: 'My Databases',
    icon: <DnsRoundedIcon />,
    link: '/databases'
  },
  {
    name: 'Register Database',
    icon: <SettingsIcon />,
    link: '/register',
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
      <List disablePadding>
        <ListItem sx={{ ...item, ...itemCategory, fontSize: 22, color: '#fff' }}>
          Gym Control Plane
        </ListItem>
        {tabs.map(({ name, icon, link }, tabId) => (
          <ListItem sx={{display: 'flex'}} disablePadding key={name}>
            <NavLink to={link} style={{ textDecoration: 'none', flex: '1' }}>
              <ListItemButton sx={item} selected={activeTabId === tabId} onClick={() => {setActiveTabId(tabId)}}>
                <ListItemIcon>{icon}</ListItemIcon>
                <ListItemText>{name}</ListItemText>
              </ListItemButton>
            </NavLink>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}