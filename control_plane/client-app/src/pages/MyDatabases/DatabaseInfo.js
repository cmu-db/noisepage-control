import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function DatabaseInfo(props) {
  const { databaseInfo: info } = props;

  const parseCreated = (created) => {
    const date = new Date(created);
    return date.toLocaleString();
  }

  return (
    <Card sx={{ minWidth: 275, mb: 4 }}>
      <CardContent>
        <Typography variant="h4">Database ID: {info.database_id}</Typography>
        <Typography>Created At: {parseCreated(info.created)}</Typography>
        <Typography>Environment Type: {info.environment_type}</Typography>
        <Typography>Active: {info.active ? 'yes' : 'no'}</Typography>
        <Typography>State: {info.state}</Typography>
        <Typography>Errors: {info.errors}</Typography>
        {info.self_managed_postgres_config && Object.keys(info.self_managed_postgres_config).map((key) => (
          <Typography key={key}>{key}: {info.self_managed_postgres_config[key]}</Typography>
        ))}
      </CardContent>
      <CardActions>
        <Button>Manage</Button>
      </CardActions>
    </Card>
  );
}
