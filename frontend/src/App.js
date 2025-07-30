import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, Box, List, ListItem, ListItemText } from '@mui/material';

const api = (path, options = {}) => fetch(`http://localhost:8000${path}`, { headers: { 'Content-Type': 'application/json' }, ...options });

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState(null);
  const [projects, setProjects] = useState([]);
  const [projectName, setProjectName] = useState('');
  const [companyDetails, setCompanyDetails] = useState('');
  const [locationId, setLocationId] = useState('');
  const [gaPropertyId, setGaPropertyId] = useState('');
  const [auditResult, setAuditResult] = useState(null);

  useEffect(() => {
    if (userId) loadProjects();
  }, [userId]);

  const register = async () => {
    const res = await api('/users/', { method: 'POST', body: JSON.stringify({ email, password }) });
    const data = await res.json();
    setUserId(data.id);
  };

  const loadProjects = async () => {
    const res = await api(`/users/${userId}/projects/`);
    const data = await res.json();
    setProjects(data);
  };

  const createProject = async () => {
    const payload = { name: projectName, company_details: companyDetails, gbp_location_id: locationId, ga_property_id: gaPropertyId };
    const res = await api(`/users/${userId}/projects/`, { method: 'POST', body: JSON.stringify(payload) });
    const data = await res.json();
    setProjects([...projects, data]);
    setProjectName('');
    setCompanyDetails('');
    setLocationId('');
    setGaPropertyId('');
  };

  const audit = async (id) => {
    const res = await api(`/projects/${id}/audit`, { method: 'POST' });
    const data = await res.json();
    setAuditResult(data);
  };

  if (!userId) {
    return (
      <Container sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>Register</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <Button variant="contained" onClick={register}>Create Account</Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Projects</Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 4 }}>
        <TextField label="Project name" value={projectName} onChange={(e) => setProjectName(e.target.value)} />
        <TextField label="Company details" value={companyDetails} onChange={(e) => setCompanyDetails(e.target.value)} />
        <TextField label="GBP location ID" value={locationId} onChange={(e) => setLocationId(e.target.value)} />
        <TextField label="GA property ID" value={gaPropertyId} onChange={(e) => setGaPropertyId(e.target.value)} />
        <Button variant="contained" onClick={createProject}>Add Project</Button>
      </Box>
      <List>
        {projects.map(p => (
          <ListItem key={p.id} secondaryAction={<Button onClick={() => audit(p.id)}>Audit</Button>}>
            <ListItemText primary={p.name} secondary={p.company_details} />
          </ListItem>
        ))}
      </List>
      {auditResult && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5">Audit Recommendations</Typography>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{auditResult.recommendations}</pre>
        </Box>
      )}

    </Container>
  );
}
