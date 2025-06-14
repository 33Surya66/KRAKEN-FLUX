import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  useTheme,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const data = [
  { time: '00:00', threats: 4, blocked: 3 },
  { time: '04:00', threats: 3, blocked: 2 },
  { time: '08:00', threats: 6, blocked: 5 },
  { time: '12:00', threats: 8, blocked: 7 },
  { time: '16:00', threats: 5, blocked: 4 },
  { time: '20:00', threats: 7, blocked: 6 },
];

const Dashboard: React.FC = () => {
  const theme = useTheme();

  const metrics = [
    {
      title: 'Active Threats',
      value: '12',
      color: theme.palette.secondary.main,
    },
    {
      title: 'Blocked Attacks',
      value: '156',
      color: theme.palette.primary.main,
    },
    {
      title: 'System Health',
      value: '98%',
      color: '#4caf50',
    },
    {
      title: 'Response Time',
      value: '0.8s',
      color: '#ff9800',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Security Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {metrics.map((metric) => (
          <Grid component="div" item key={metric.title} xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  {metric.title}
                </Typography>
                <Typography variant="h4" component="div" sx={{ color: metric.color }}>
                  {metric.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}

        <Grid component="div" item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Threat Activity
              </Typography>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="threats"
                      stroke={theme.palette.secondary.main}
                      name="Threats Detected"
                    />
                    <Line
                      type="monotone"
                      dataKey="blocked"
                      stroke={theme.palette.primary.main}
                      name="Threats Blocked"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 