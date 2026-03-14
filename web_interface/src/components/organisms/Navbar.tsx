import Link from 'next/link';
import { Button } from '@/components/ui/button';

export const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-2">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
              CareerPulse
            </span>
          </Link>
        </div>
        <div className="hidden md:flex items-center gap-6 text-sm font-medium">
          <Link href="/upload" className="hover:text-primary transition-colors">
            Analyze Resume
          </Link>
          <Link href="/dashboard" className="hover:text-primary transition-colors">
            Dashboard
          </Link>
          <Button variant="outline" size="sm">
            Sign In
          </Button>
        </div>
      </div>
    </nav>
  );
};
