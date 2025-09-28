import { useState } from 'react';
import { Heading, Stack, Input, Button, useToast } from '@chakra-ui/react';
import { apiFetch } from '../lib/api';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      const data = await apiFetch<{ access_token: string }>('/auth/login', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      if (data?.access_token) {
        localStorage.setItem('token', data.access_token);
      }
      toast({ title: 'Inicio de sesión exitoso', status: 'success' });
    } catch (error) {
      toast({ title: 'Error al iniciar sesión', status: 'error' });
    }
  };

  return (
    <Stack spacing={4}>
      <Heading>Iniciar sesión</Heading>
      <Input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <Input placeholder="Contraseña" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <Button onClick={handleLogin}>Ingresar</Button>
    </Stack>
  );
};

export default LoginPage;
