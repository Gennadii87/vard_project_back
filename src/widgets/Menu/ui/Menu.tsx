import { MenuItem } from '@/shared/ui/model/MenuItem';
import { IMenuItem } from '../types/menu.interface';
import { FC } from 'react';

export const Menu: FC<{ items: IMenuItem[] }> = ({ items }) => {
	return (
		<ul>
			{items.map(item => (
				<MenuItem key={item.title} {...item} />
			))}
		</ul>
	);
};
