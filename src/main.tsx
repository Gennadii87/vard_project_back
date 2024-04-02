import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.scss';
import { RootProvider } from './app/provides/RootProvider';
import { RouterProvider } from 'react-router-dom';
import { router } from '@/shared/config/router.config';

const container = document.getElementById('root');

if (container) {
	const root = createRoot(container);

	root.render(
		<React.StrictMode>
			<RootProvider>
				<RouterProvider router={router} />
			</RootProvider>
		</React.StrictMode>,
	);
} else {
	throw new Error(
		"Root element with ID 'root' not found in the document. Ensure there is a corresponding HTML element with the ID 'root' in your HTML file.",
	);
}

