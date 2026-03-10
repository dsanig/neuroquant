'use client';

type FilterBarProps = {
  search: string;
  onSearchChange: (value: string) => void;
  strategy: string;
  strategyOptions: string[];
  onStrategyChange: (value: string) => void;
  sort: string;
  sortOptions: Array<{ label: string; value: string }>;
  onSortChange: (value: string) => void;
};

export function FilterBar({
  search,
  onSearchChange,
  strategy,
  strategyOptions,
  onStrategyChange,
  sort,
  sortOptions,
  onSortChange,
}: FilterBarProps) {
  return (
    <div className="filter-bar card" role="search">
      <label>
        <span className="subtle">Search</span>
        <input
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Symbol, ID, side"
          aria-label="Search records"
        />
      </label>
      <label>
        <span className="subtle">Strategy</span>
        <select value={strategy} onChange={(e) => onStrategyChange(e.target.value)} aria-label="Filter strategy">
          <option value="all">All strategies</option>
          {strategyOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
      <label>
        <span className="subtle">Sort</span>
        <select value={sort} onChange={(e) => onSortChange(e.target.value)} aria-label="Sort records">
          {sortOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
