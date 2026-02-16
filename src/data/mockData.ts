import { Student, StudentMessage } from '../types/student';

export const mockStudents: Student[] = [
  {
    id: '1',
    name: 'Alex Johnson',
    riskScore: 75,
    lastLogin: '2024-01-15T10:30:00Z',
  },
  {
    id: '2',
    name: 'Sarah Williams',
    riskScore: 45,
    lastLogin: '2024-01-16T14:20:00Z',
  },
  {
    id: '3',
    name: 'Michael Chen',
    riskScore: 88,
    lastLogin: '2024-01-12T09:15:00Z',
  },
  {
    id: '4',
    name: 'Emily Davis',
    riskScore: 32,
    lastLogin: '2024-01-16T16:45:00Z',
  },
  {
    id: '5',
    name: 'David Martinez',
    riskScore: 92,
    lastLogin: '2024-01-10T11:00:00Z',
  },
];

export const mockStudentMessage: StudentMessage = {
  studentName: 'Alex',
  message: 'Hi Alex, we noticed you missed 2 assignments. Need help?',
};

