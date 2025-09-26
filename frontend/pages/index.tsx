import { useEffect, useState } from 'react';
import { Heading, SimpleGrid, Select, Stack, Spinner, useToast } from '@chakra-ui/react';
import api from '../lib/api';
import CallCard from '../components/CallCard';

const HomePage = () => {
  const [calls, setCalls] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [country, setCountry] = useState<string>('');
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
  }, []);

  const handleFavorite = async (id: number) => {
    toast({ title: 'Favoritos requieren login', status: 'info' });
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
            <CallCard key={call.id} call={call} onFavorite={handleFavorite} />
          ))}
        </SimpleGrid>
      )}
    </Stack>
  );
};

export default HomePage;
