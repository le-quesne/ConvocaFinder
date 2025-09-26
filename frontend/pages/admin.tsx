import { useEffect, useState } from 'react';
import { Heading, Table, Thead, Tbody, Tr, Th, Td, Spinner, Stack, useToast } from '@chakra-ui/react';
import api from '../lib/api';

const AdminPage = () => {
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const toast = useToast();

  const fetchSources = async () => {
    setLoading(true);
    try {
      const response = await api.get('/sources');
      setSources(response.data);
    } catch (error) {
      toast({ title: 'Error cargando fuentes', status: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSources();
  }, []);

  return (
    <Stack spacing={4}>
      <Heading>Panel de fuentes</Heading>
      {loading ? <Spinner /> : (
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Nombre</Th>
              <Th>Método</Th>
              <Th>Frecuencia (h)</Th>
              <Th>robots.txt</Th>
            </Tr>
          </Thead>
          <Tbody>
            {sources.map((source) => (
              <Tr key={source.id}>
                <Td>{source.name}</Td>
                <Td>{source.access_method}</Td>
                <Td>{source.frequency_hours}</Td>
                <Td>{source.robots_status}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      )}
    </Stack>
  );
};

export default AdminPage;
