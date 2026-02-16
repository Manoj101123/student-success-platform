import React from 'react';
import { Container, Typography, Paper, Box, Alert } from '@mui/material';
import { mockStudentMessage } from '../data/mockData';

export default function StudentPage() {
  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Student Portal
      </Typography>
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Alert severity="info">
            <Typography variant="h6" gutterBottom>
              Personalized Message
            </Typography>
            <Typography variant="body1">
              {mockStudentMessage.message}
            </Typography>
          </Alert>
        </Paper>
      </Box>
    </Container>
  );
}
