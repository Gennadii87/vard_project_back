import { NavItems } from '@/shared/ui/model/NavItems';
import { NavUser } from '@/shared/ui/model/NavUser';
import { FC } from 'react';

import styles from './Navbar.module.scss'

export const Navbar: FC = () => {
	return (
		<nav className={styles.navbar}>
			<NavItems />
			<NavUser />
		</nav>
	);
};
