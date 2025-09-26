import { useEffect, useState } from 'react';
import { Heading, Table, Thead, Tbody, Tr, Th, Td, Spinner, Stack, useToast } from '@chakra-ui/react';
import api from '../lib/api';

interface Source {
  id: number;
  name: string;
  access_method: string;
  frequency_hours: number;
  robots_status: string;
}

interface ScrapeLog {
  id: number;
  started_at: string;
  finished_at?: string;
  status: string;
  items_fetched: number;
  items_created: number;
  items_updated: number;
  error_message?: string;
}

interface SourceScrapeLog {
  source: Source;
  log: ScrapeLog | null;
}

const AdminPage = () => {
  const [scrapeLogs, setScrapeLogs] = useState<SourceScrapeLog[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const toast = useToast();

  const fetchScrapeLogs = async () => {
    setLoading(true);
    try {
      const response = await api.get('/scrape-logs');
      setScrapeLogs(response.data);
    } catch (error) {
      toast({ title: 'Error cargando registros', status: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) {
      return '—';
    }
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatItems = (log?: ScrapeLog | null) => {
    if (!log) {
      return '—';
    }
    return `${log.items_fetched}/${log.items_created}/${log.items_updated}`;
  };

  useEffect(() => {
    fetchScrapeLogs();
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
              <Th>Última ejecución</Th>
              <Th>Items (F/C/U)</Th>
              <Th>Error</Th>
            </Tr>
          </Thead>
          <Tbody>
            {scrapeLogs.map(({ source, log }) => (
              <Tr key={source.id}>
                <Td>{source.name}</Td>
                <Td>{source.access_method}</Td>
                <Td>{source.frequency_hours}</Td>
                <Td>{source.robots_status}</Td>
                <Td>{log ? formatDate(log.finished_at || log.started_at) : 'Sin registros'}</Td>
                <Td>{formatItems(log)}</Td>
                <Td>{log?.error_message || '—'}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      )}
    </Stack>
  );
};

export default AdminPage;
