import {
	getChartsUrl,
	getCommunityUrl,
	getConnectionsUrl,
	getDashboardsUrl,
	getFilesUrl,
	getPracticesUrl,
	getWikiUrl,
} from '@/shared/config/url.config';
import { IMenuItem } from '@/widgets/Menu/types/menu.interface';

export const UserData: IMenuItem[] = [
	{
		title: 'Dashboards',
		icon: '/sidebar/dashboards.svg',
		link: getDashboardsUrl(),
	},
	{
		title: 'Connections',
		icon: '/sidebar/connections.svg',
		link: getConnectionsUrl(),
	},
	{
		title: 'Files',
		icon: '/sidebar/files.svg',
		link: getFilesUrl(),
	},
	{
		title: 'Charts',
		icon: '/sidebar/charts.svg',
		link: getChartsUrl(),
	},
	{
		title: 'Wiki',
		icon: '/sidebar/wiki.svg',
		link: getWikiUrl(),
	},
];

export const CommunityData: IMenuItem[] = [
	{
		title: 'Best Practices',
		icon: '/sidebar/practices.svg',
		link: getPracticesUrl(),
	},
	{
		title: 'Community',
		icon: '/sidebar/community.svg',
		link: getCommunityUrl(),
	},
];
