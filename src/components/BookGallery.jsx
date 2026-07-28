export default function BookGallery ({children})  {
    return (
        <div className="row row-cols-1 row-cols-md-4 g-4">{children}</div>
    );
}