function UserPageHeader({ title, description }) {
  return <header className="mb-6"><h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">{title}</h1><p className="mt-2 text-sm leading-6 text-slate-500">{description}</p></header>;
}
export default UserPageHeader;
