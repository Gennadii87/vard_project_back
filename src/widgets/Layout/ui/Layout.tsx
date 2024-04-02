import { Header } from '@/widgets/Header';
import { Sidebar } from '@/widgets/Sidebar';
import { FC } from 'react';
import { Outlet } from 'react-router-dom';

export const Layout: FC = () => {
	return (
		<>
			<Header />
			<div style={{ display: 'flex' }}>
				<Sidebar />
				<Outlet />
			</div>
		</>
	);
};
