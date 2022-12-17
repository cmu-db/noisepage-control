import { Link } from 'react-router-dom';
import Card from '@mui/material/Card';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import DatabaseRegisterState from '../../util/databaseRegisterState';
import parseDateTime from '../../util/parseDateTime';
import databaseDetails from '../../fixtures/databaseDetail';

export default function DatabaseInfo(props) {
  const { databaseInfo: info } = props;

  const getStateColor = (state) => {
    switch (DatabaseRegisterState[state]) {
      case DatabaseRegisterState.HEALTHY:
        return 'success.main';
      case DatabaseRegisterState.UNHEALTHY:
        return 'error';
      default:
        return 'warning.light';
    }
  }

  return (
    <Card sx={{ minWidth: 275, mb: 4, p: 1, display: 'flex', alignItems: 'center' }}>
      <img
        src={'/postgres.png'}
        alt="pg-logo"
        style={{ width: '100px', height: '100px', paddingLeft: '24px', objectFit: 'contain' }}
      />
      <Grid container spacing={2} alignItems="center" sx={{ p: 2, px: 3 }} >
        <Grid item xs={12} md={9}>
          <Typography variant="h4" pt={1}>
            {/* TODO: uncoment this Database ID: {info.database_id} */}
            <Link to={`/databases/${info.database_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
              {databaseDetails[info.database_id].Name}
            </Link>
          </Typography>
        </Grid>
        <Grid item xs={12} md={3} sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="h6">State: &nbsp;</Typography>
          <Typography variant="h6" color={getStateColor(info.state)}>{DatabaseRegisterState[info.state]}</Typography>
          {DatabaseRegisterState[info.state] === DatabaseRegisterState.REGISTERING &&
            <CircularProgress disableShrink size={15} sx={{
                ml: 1, opacity: 0.5, color: '#2e7d32'
              }}
            />
          }
        </Grid>
        <Grid item xs={12} md={9}>
          <Grid container alignItems="center">
            <Grid item xs={9}>
              {
                Object.keys(databaseDetails[info.database_id]).map(key => {
                  if (key === 'Name') {
                    return null;
                  }
                  return (
                    <Typography variant="caption" color='GrayText' display="block" key={`${info.database_id}_${key}`}>
                      {key}: {databaseDetails[info.database_id][key]}
                    </Typography>
                  )
                })
              }
            </Grid>
            <Grid item xs={3}>
              <Link to={`/databases/${info.database_id}`}>
                <Button
                  variant="contained"
                  disabled={DatabaseRegisterState[info.state] !== DatabaseRegisterState.HEALTHY}
                >Manage</Button>
              </Link>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={3}>
          {/* TODO: add this line back */}
          {/* <Typography sx={{ fontSize: '0.9rem', pt: 0 }}>Registered On: {parseDateTime(info.created)}</Typography> */}
          <Typography sx={{ fontSize: '0.9rem', pt: 0 }}>Registered On: {databaseDetails[info.database_id]['Registered']}</Typography>
        </Grid>
      </Grid>
    </Card>
  );
}
