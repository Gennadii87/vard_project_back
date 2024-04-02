import { Menu } from '@/widgets/Menu';
import { UserData, CommunityData } from '../model/sidebar.data';
import { FC } from 'react';

import styles from './Sidebar.module.scss'

export const Sidebar: FC = () => {
	return (
		<div className={styles.sidebar}>
			<Menu items={UserData} />
			<Menu items={CommunityData} />
		</div>
	);
};
