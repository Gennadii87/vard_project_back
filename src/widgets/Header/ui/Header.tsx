import { FC } from 'react';

import styles from './Header.module.scss';
import { Navbar } from '@/widgets/Navbar';
import { Logo } from '@/shared/ui/ui/Logo'

export const Header: FC = () => {
	return (
		<header className={styles.header}>
			<Logo />
			<Navbar />
		</header>
	);
};
