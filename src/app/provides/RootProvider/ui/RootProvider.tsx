import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FC, ReactNode, useState } from 'react';

export const RootProvider: FC<{ children: ReactNode }> = ({ children }) => {
	const [queryClient] = useState(
		new QueryClient({
			defaultOptions: {
				queries: {
					refetchOnWindowFocus: false,
				},
			},
		}),
	);

	return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};
