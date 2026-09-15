function PageContainer({ children }) {
  return (
    <main className="min-h-[calc(100vh-5rem)] bg-slate-50 lg:ml-64">
      <div className="mx-auto w-full max-w-[1800px] px-4 py-6 md:px-6 lg:px-8">
        {children}
      </div>
    </main>
  );
}

export default PageContainer;
