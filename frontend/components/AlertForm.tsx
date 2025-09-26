import { ChangeEvent, FormEvent, useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
  SimpleGrid,
  Stack,
  useToast,
} from '@chakra-ui/react';
import api from '../lib/api';

type AlertFilters = {
  country: string;
  industry: string;
  amount_min: string;
  amount_max: string;
  stage: string;
  closing_before: string;
  closing_after: string;
  funding_type: string;
};

export type Alert = {
  id: number;
  channel: string;
  filters: Record<string, unknown>;
  is_active: boolean;
};

type AlertFormProps = {
  onAlertCreated?: (alert: Alert) => void;
};

const initialFilters: AlertFilters = {
  country: '',
  industry: '',
  amount_min: '',
  amount_max: '',
  stage: '',
  closing_before: '',
  closing_after: '',
  funding_type: '',
};

const AlertForm = ({ onAlertCreated }: AlertFormProps) => {
  const [filters, setFilters] = useState<AlertFilters>(initialFilters);
  const [channel, setChannel] = useState<string>('email');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const toast = useToast();

  const hasToken = typeof window !== 'undefined' && Boolean(localStorage.getItem('token'));

  const handleInputChange = (field: keyof AlertFilters) => (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFilters((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const resetForm = () => {
    setFilters(initialFilters);
    setChannel('email');
  };

  const buildPayload = () => {
    const parsedFilters: Record<string, string | number> = {};

    Object.entries(filters).forEach(([key, value]) => {
      if (!value) {
        return;
      }

      if (key === 'amount_min' || key === 'amount_max') {
        const numberValue = parseFloat(value);
        if (!Number.isNaN(numberValue)) {
          parsedFilters[key] = numberValue;
        }
        return;
      }

      parsedFilters[key] = value;
    });

    return {
      filters: parsedFilters,
      channel,
    };
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (typeof window === 'undefined') {
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      toast({
        title: 'Debes iniciar sesión para crear alertas',
        status: 'warning',
      });
      return;
    }

    const payload = buildPayload();

    setIsSubmitting(true);
    try {
      const response = await api.post('/alerts', payload, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      toast({ title: 'Alerta creada correctamente', status: 'success' });
      resetForm();
      if (onAlertCreated) {
        onAlertCreated(response.data);
      }
    } catch (error) {
      toast({ title: 'No se pudo crear la alerta', status: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Box as="form" onSubmit={handleSubmit} borderWidth="1px" borderRadius="md" p={4}>
      <Stack spacing={4}>
        <Heading as="h2" size="md">
          Crea una alerta personalizada
        </Heading>
        {!hasToken && (
          <Box color="orange.600" fontSize="sm">
            Necesitas iniciar sesión para guardar alertas.
          </Box>
        )}
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
          <FormControl>
            <FormLabel>País</FormLabel>
            <Input value={filters.country} onChange={handleInputChange('country')} placeholder="Ej. Chile" />
          </FormControl>
          <FormControl>
            <FormLabel>Industria</FormLabel>
            <Input value={filters.industry} onChange={handleInputChange('industry')} placeholder="Ej. Tecnología" />
          </FormControl>
          <FormControl>
            <FormLabel>Monto mínimo</FormLabel>
            <Input type="number" value={filters.amount_min} onChange={handleInputChange('amount_min')} placeholder="Ej. 10000" />
          </FormControl>
          <FormControl>
            <FormLabel>Monto máximo</FormLabel>
            <Input type="number" value={filters.amount_max} onChange={handleInputChange('amount_max')} placeholder="Ej. 50000" />
          </FormControl>
          <FormControl>
            <FormLabel>Etapa</FormLabel>
            <Input value={filters.stage} onChange={handleInputChange('stage')} placeholder="Ej. Seed" />
          </FormControl>
          <FormControl>
            <FormLabel>Tipo de financiamiento</FormLabel>
            <Input value={filters.funding_type} onChange={handleInputChange('funding_type')} placeholder="Ej. Subsidio" />
          </FormControl>
          <FormControl>
            <FormLabel>Cierra antes de</FormLabel>
            <Input type="date" value={filters.closing_before} onChange={handleInputChange('closing_before')} />
          </FormControl>
          <FormControl>
            <FormLabel>Cierra después de</FormLabel>
            <Input type="date" value={filters.closing_after} onChange={handleInputChange('closing_after')} />
          </FormControl>
        </SimpleGrid>
        <FormControl>
          <FormLabel>Canal</FormLabel>
          <Select value={channel} onChange={(event) => setChannel(event.target.value)}>
            <option value="email">Email</option>
          </Select>
        </FormControl>
        <Button type="submit" colorScheme="blue" isLoading={isSubmitting}>
          Guardar alerta
        </Button>
      </Stack>
    </Box>
  );
};

export default AlertForm;
