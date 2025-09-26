import { useState } from 'react';
import { useRouter } from 'next/router';
import {
  Heading,
  Stack,
  Input,
  Button,
  useToast,
  Text,
  Link as ChakraLink
} from '@chakra-ui/react';
import NextLink from 'next/link';
import api from '../lib/api';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const RegisterPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const toast = useToast();
  const router = useRouter();

  const handleRegister = async () => {
    if (!email || !password) {
      toast({ title: 'Por favor completa todos los campos.', status: 'warning' });
      return;
    }

    if (!emailRegex.test(email)) {
      toast({ title: 'Ingresa un email válido.', status: 'warning' });
      return;
    }

    try {
      setIsSubmitting(true);
      await api.post('/auth/register', { email, password });
      toast({ title: 'Registro exitoso. Inicia sesión para continuar.', status: 'success' });
      router.push('/login');
    } catch (error) {
      toast({ title: 'Error al registrarse. Intenta nuevamente.', status: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Stack spacing={4}>
      <Heading>Crear cuenta</Heading>
      <Input
        placeholder="Email"
        value={email}
        type="email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <Input
        placeholder="Contraseña"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button onClick={handleRegister} isLoading={isSubmitting}>
        Registrarse
      </Button>
      <Text textAlign="center">
        ¿Ya tienes una cuenta?{' '}
        <ChakraLink as={NextLink} href="/login" color="teal.500">
          Inicia sesión
        </ChakraLink>
      </Text>
    </Stack>
  );
};

export default RegisterPage;
