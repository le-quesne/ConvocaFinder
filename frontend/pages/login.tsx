import { useState } from 'react';
import { Heading, Stack, Input, Button, useToast, Text, Link as ChakraLink } from '@chakra-ui/react';
import NextLink from 'next/link';
import api from '../lib/api';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      const response = await api.post('/auth/login', formData);
      localStorage.setItem('token', response.data.access_token);
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
      <Text textAlign="center">
        ¿No tienes cuenta?{' '}
        <ChakraLink as={NextLink} href="/register" color="teal.500">
          Regístrate
        </ChakraLink>
      </Text>
    </Stack>
  );
};

export default LoginPage;
