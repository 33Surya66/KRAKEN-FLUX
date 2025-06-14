import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  useTheme,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const threats = [
  {
    id: 1,
    timestamp: '2024-03-20 14:30:22',
    type: 'SQL Injection',
    severity: 'High',
    source: '192.168.1.100',
    status: 'Blocked',
  },
  {
    id: 2,
    timestamp: '2024-03-20 14:29:15',
    type: 'XSS Attack',
    severity: 'Medium',
    source: '192.168.1.101',
    status: 'Blocked',
  },
  {
    id: 3,
    timestamp: '2024-03-20 14:28:45',
    type: 'DDoS Attempt',
    severity: 'Critical',
    source: '192.168.1.102',
    status: 'Mitigated',
  },
  {
    id: 4,
    timestamp: '2024-03-20 14:27:30',
    type: 'Brute Force',
    severity: 'High',
    source: '192.168.1.103',
    status: 'Blocked',
  },
];

const ThreatDetection: React.FC = () => {
  const theme = useTheme();

  const columns: GridColDef[] = [
    { field: 'timestamp', headerName: 'Timestamp', width: 180 },
    { field: 'type', headerName: 'Threat Type', width: 150 },
    {
      field: 'severity',
      headerName: 'Severity',
      width: 120,
      renderCell: (params) => (
        <Typography
          sx={{
            color:
              params.value === 'Critical'
                ? theme.palette.error.main
                : params.value === 'High'
                ? theme.palette.warning.main
                : theme.palette.info.main,
          }}
        >
          {params.value}
        </Typography>
      ),
    },
    { field: 'source', headerName: 'Source IP', width: 150 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Typography
          sx={{
            color:
              params.value === 'Blocked'
                ? theme.palette.success.main
                : theme.palette.warning.main,
          }}
        >
          {params.value}
        </Typography>
      ),
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Threat Detection
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Active Threats Overview
          </Typography>
          <Box sx={{ height: 400, width: '100%' }}>
            <DataGrid
              rows={threats}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: { pageSize: 5, page: 0 },
                },
              }}
              pageSizeOptions={[5]}
              disableRowSelectionOnClick
              sx={{
                backgroundColor: theme.palette.background.paper,
                '& .MuiDataGrid-cell': {
                  borderColor: theme.palette.divider,
                },
                '& .MuiDataGrid-columnHeaders': {
                  backgroundColor: theme.palette.background.default,
                },
              }}
            />
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ThreatDetection; 