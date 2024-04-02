import { NavItemData } from '../model/nav-items.data';
import { FC } from 'react';

import styles from './NavItems.module.scss';

export const NavItems: FC = () => {
	return (
		<ul className={styles['nav-items']}>
			{NavItemData.map(item => (
				<li key={item.title}>
					<button>
						<img src={item.icon} width={18} height={18} alt={`Icon ${item.title}`} />
					</button>
				</li>
			))}
		</ul>
	);
};
