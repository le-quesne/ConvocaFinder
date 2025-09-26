import { useEffect, useState } from 'react';
import { Box, Heading, SimpleGrid, Select, Stack, Spinner, Text, useToast } from '@chakra-ui/react';
import api from '../lib/api';
import CallCard from '../components/CallCard';
import AlertForm, { Alert } from '../components/AlertForm';

const HomePage = () => {
  const [calls, setCalls] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [country, setCountry] = useState<string>('');
  const [alerts, setAlerts] = useState<Alert[]>([]);
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
      <AlertForm
        onAlertCreated={(alert) => {
          setAlerts((prev) => {
            const exists = prev.some((item) => item.id === alert.id);
            if (exists) {
              return prev.map((item) => (item.id === alert.id ? alert : item));
            }
            return [alert, ...prev];
          });
        }}
      />
      {alerts.length > 0 && (
        <Stack spacing={2}>
          <Heading as="h3" size="md">
            Tus alertas recientes
          </Heading>
          {alerts.map((alert) => (
            <Box key={alert.id} borderWidth="1px" borderRadius="md" p={3}>
              <Text fontWeight="bold">Canal: {alert.channel}</Text>
              <Text fontSize="sm" color="gray.600">
                {alert.filters && Object.keys(alert.filters).length > 0
                  ? Object.entries(alert.filters)
                      .map(([key, value]) => {
                        if (Array.isArray(value)) {
                          return `${key}: ${value.join(', ')}`;
                        }
                        return `${key}: ${String(value)}`;
                      })
                      .join(', ')
                  : 'Sin filtros específicos'}
              </Text>
            </Box>
          ))}
        </Stack>
      )}
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
