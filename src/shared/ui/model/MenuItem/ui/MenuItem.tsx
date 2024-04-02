import { IMenuItem } from '@/widgets/Menu/types/menu.interface';
import { FC } from 'react';
import cn from '@/shared/lib/classNames';

import styles from './MenuItem.module.scss';
import { Link, useLocation } from 'react-router-dom';

export const MenuItem: FC<IMenuItem> = ({ title, icon, link }) => {
	const { pathname } = useLocation();

	return (
		<li
			className={cn(
				styles.item,
				{
					[styles.active]: pathname === link,
				},
				[],
			)}
		>
			<Link to={link}>
				<img src={icon} width={32} height={32} alt={`Icon ${title}`} />
				{title}
			</Link>
		</li>
	);
};
