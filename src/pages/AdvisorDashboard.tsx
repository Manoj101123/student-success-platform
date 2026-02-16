import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import { mockStudents } from '../data/mockData';

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return 'Invalid date';
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function getRiskColor(score: number): 'error' | 'warning' | 'success' {
  if (score >= 70) return 'error';
  if (score >= 50) return 'warning';
  return 'success';
}

export default function AdvisorDashboard() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Advisor Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Student Overview and Risk Assessment
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Name</strong></TableCell>
              <TableCell><strong>Risk Score</strong></TableCell>
              <TableCell><strong>Last Login</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {mockStudents.map((student) => (
              <TableRow key={student.id} hover>
                <TableCell>{student.name}</TableCell>
                <TableCell>
                  <Chip
                    label={`${student.riskScore}%`}
                    color={getRiskColor(student.riskScore)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{formatDate(student.lastLogin)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}
