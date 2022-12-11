import * as React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import HelpIcon from '@mui/icons-material/Help';
import IconButton from '@mui/material/IconButton';
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import NotificationsIcon from '@mui/icons-material/Notifications';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Toolbar from '@mui/material/Toolbar';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';

const lightColor = 'rgba(255, 255, 255, 0.7)';

function Header({ title, icon }) {
  // const { onDrawerToggle } = props;

  return (
    <React.Fragment>
      <AppBar
        component="div"
        color="primary"
        position="static"
        elevation={0}
        sx={{
          zIndex: 0,
          py: 3,
          px: 3
        }}
      >
        <Typography color="inherit" variant="h5" component="h1" sx={{ display: 'flex', alignItems: 'center' }}>
          {icon}
          {title}
        </Typography>

      </AppBar>
    </React.Fragment>
  );
}

Header.propTypes = {
  // onDrawerToggle: PropTypes.func.isRequired,
  title: PropTypes.string.isRequired
};

export default Header;