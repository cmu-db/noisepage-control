import * as React from 'react';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import { Link as RouterLink } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';

export default function MyBreadCrumbs({ databaseId }) {
  const breadcrumbs = [
    <Link underline="hover" component={RouterLink} to="/databases">
      <Typography fontWeight={500}>
        View Databases
      </Typography>
    </Link>,
    <Typography key="3" color="gray" fontWeight={500}>
      {databaseId}
    </Typography>,
  ];

  return (
    <Stack spacing={2}>
      <Breadcrumbs
        separator={<NavigateNextIcon fontSize="small" />}
        aria-label="breadcrumb"
      >
        {breadcrumbs}
      </Breadcrumbs>
    </Stack>
  );
};
