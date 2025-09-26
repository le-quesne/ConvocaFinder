import { useEffect, useState } from 'react';
import { Heading, SimpleGrid, Select, Stack, Spinner, useToast } from '@chakra-ui/react';
import axios from 'axios';
import api from '../lib/api';
import CallCard from '../components/CallCard';

const HomePage = () => {
  const [calls, setCalls] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [country, setCountry] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const toast = useToast();

  const fetchCalls = async (filters: any = {}) => {
    setLoading(true);
    try {
      const response = await api.get('/convocatorias', { params: filters });
      setCalls(response.data.data);
    } catch (error) {
      toast({ title: 'Error cargando convocatorias', status: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalls();
    if (typeof window !== 'undefined') {
      const updateAuthState = () => {
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);
      };

      updateAuthState();
      window.addEventListener('auth:logout', updateAuthState);
      window.addEventListener('storage', updateAuthState);

      return () => {
        window.removeEventListener('auth:logout', updateAuthState);
        window.removeEventListener('storage', updateAuthState);
      };
    }
  }, []);

  const handleFavorite = async (id: number) => {
    if (!isAuthenticated) {
      toast({ title: 'Inicia sesión para guardar favoritos', status: 'info' });
      return;
    }

    try {
      await api.post(`/convocatorias/${id}/favorite`);
      toast({ title: 'Convocatoria agregada a favoritos', status: 'success' });
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        toast({ title: 'Tu sesión ha expirado, vuelve a iniciar sesión', status: 'warning' });
      } else {
        toast({ title: 'No se pudo agregar a favoritos', status: 'error' });
      }
    }
  };

  return (
    <Stack spacing={4}>
      <Heading>ConvocaFinder</Heading>
      <Select placeholder="Filtrar por país" value={country} onChange={(e) => {
        setCountry(e.target.value);
        fetchCalls({ country: e.target.value });
      }}>
        <option value="Chile">Chile</option>
        <option value="México">México</option>
        <option value="Colombia">Colombia</option>
      </Select>
      {loading ? <Spinner /> : (
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
          {calls.map((call) => (
            <CallCard
              key={call.id}
              call={call}
              onFavorite={handleFavorite}
              canFavorite={isAuthenticated}
            />
          ))}
        </SimpleGrid>
      )}
    </Stack>
  );
};

export default HomePage;
