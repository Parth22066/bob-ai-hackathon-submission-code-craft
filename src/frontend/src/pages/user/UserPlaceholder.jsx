function UserPlaceholder({ icon: Icon, title, description }) {
  return <section className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm sm:p-10"><div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600"><Icon size={24} /></div><h1 className="mt-6 text-2xl font-bold tracking-tight text-slate-900">{title}</h1><p className="mt-3 max-w-xl leading-7 text-slate-500">{description}</p><div className="mt-8 rounded-xl border border-dashed border-slate-200 bg-slate-50 px-4 py-5 text-sm text-slate-500">This section is ready for the next phase of the customer portal.</div></section>;
}

export default UserPlaceholder;
